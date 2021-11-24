package commands

import (
	"errors"
	"fmt"
	"github.com/jfrog/jfrog-cli-core/v2/common/commands"
	"github.com/jfrog/jfrog-cli-core/v2/plugins/components"
	"github.com/jfrog/jfrog-cli-core/v2/utils/config"
	clientutils "github.com/jfrog/jfrog-client-go/utils"
	"github.com/jfrog/jfrog-client-go/utils/log"

	"os/exec"
)

const ServerIdFlag = "server-id"

func GetAutosetupCommand() components.Command {
	return components.Command{
		Name:        "autosetup",
		Description: "Automatically setup your machine to work with a remote Artifactory repo.",
		Flags:       getFlags(),
		Action: func(c *components.Context) error {
			return autosetupCmd(c)
		},
	}
}

func getFlags() []components.Flag {
	return []components.Flag{
		components.StringFlag{
			Name:        ServerIdFlag,
			Description: "Artifactory server ID configured using the config command. Leave empty for default.",
		},
	}
}

func autosetupCmd(c *components.Context) error {
	var args = c.Arguments

	details, err := getRtDetails(c)
	if err != nil {
		return err
	}

	args = append(
		[]string{
			"commands/autosetup.py",
			"autosetup",
			"--username",
			details.User,
			"--password",
			details.Password,
			"--server-url",
			details.Url,
		},
		args...,
	)
	log.Output(args)

	//out, err := exec.Command("python3", args...).Output()
	out, err := exec.Command("python", args...).Output()
	if err != nil {
		log.Output(err)
		log.Output(out)
		return nil
	}

	log.Output(fmt.Sprintf("%s", out))
	return nil
}

// Returns the Artifactory Details of the provided server-id, or the default one.
func getRtDetails(c *components.Context) (*config.ServerDetails, error) {
	serverId := c.GetStringFlagValue(ServerIdFlag)
	details, err := commands.GetConfig(serverId, false)

	if err != nil {
		return nil, err
	}

	if details.Url == "" {
		return nil, errors.New("no server-id was found, or the server-id has no url")
	}

	details.Url = clientutils.AddTrailingSlashIfNeeded(details.Url)
	err = config.CreateInitialRefreshableTokensIfNeeded(details)

	if err != nil {
		return nil, err
	}

	return details, nil
}
