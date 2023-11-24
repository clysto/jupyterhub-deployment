package main

import (
	"bytes"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"text/template"

	_ "github.com/mattn/go-sqlite3"
	log "github.com/sirupsen/logrus"
	"github.com/tg123/sshpiper/libplugin"
	"github.com/urfave/cli/v2"
)

var db *sql.DB

func getHostPort(templ *template.Template, username string) (string, int, error) {
	buf := &bytes.Buffer{}
	err := templ.Execute(
		buf, map[string]string{"User": username})
	if err != nil {
		return "", 0, err
	}
	target := buf.String()
	host, port, err := libplugin.SplitHostPortForSSH(target)
	if err != nil {
		return "", 0, err
	}
	return host, port, nil
}

func loadPrivateKeyAndCert(hash string) ([]byte, []byte, string, error) {
	query := "SELECT private_key, certificate, username FROM user_keys WHERE fingerprint = ?"
	stmt, err := db.Prepare(query)
	if err != nil {
		return nil, nil, "", err
	}
	defer stmt.Close()
	row := stmt.QueryRow(hash)
	var privateKey []byte
	var certificate []byte
	var username string
	err = row.Scan(&privateKey, &certificate, &username)
	if err != nil {
		return nil, nil, "", err
	}
	return privateKey, certificate, username, nil
}

func main() {
	libplugin.CreateAndRunPluginTemplate(&libplugin.PluginTemplate{
		Name:  "sshmux",
		Usage: "sshpiperd sshmux plugin, redirect to a host with a template",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "template",
				Usage:    "template string used to sshmux host",
				EnvVars:  []string{"SSHPIPERD_SSHMUX_TEMPLATE"},
				Required: true,
			},
			&cli.StringFlag{
				Name:     "db",
				Usage:    "database file",
				EnvVars:  []string{"SSHPIPERD_SSHMUX_DB"},
				Required: true,
			},
		},
		CreateConfig: func(c *cli.Context) (*libplugin.SshPiperPluginConfig, error) {
			templateStr := c.String("template")
			dbFile := c.String("db")
			targetTemplate, err := template.New("target").Parse(templateStr)

			if err != nil {
				return nil, err
			}

			db, err = sql.Open("sqlite3", dbFile)
			if err != nil {
				return nil, err
			}

			return &libplugin.SshPiperPluginConfig{
				PublicKeyCallback: func(conn libplugin.ConnMetadata, key []byte) (*libplugin.Upstream, error) {
					user := conn.User()
					hash := sha256.Sum256(key)
					hashStr := hex.EncodeToString(hash[:])
					log.Info("pubkey hash ", hashStr)
					signer, capublickey, username, err := loadPrivateKeyAndCert(hashStr)
					if err != nil {
						return nil, err
					}
					host, port, err := getHostPort(targetTemplate, username)
					if err != nil {
						return nil, err
					}
					log.Info("routing to ", host, ":", port)
					return &libplugin.Upstream{
						Host:          host,
						Port:          int32(port),
						IgnoreHostKey: true,
						UserName:      user,
						Auth:          libplugin.CreatePrivateKeyAuth(signer, capublickey),
					}, nil
				},
			}, nil
		},
	})
}
