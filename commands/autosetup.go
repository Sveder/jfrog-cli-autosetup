package commands

import (
	"errors"
	"fmt"
	"github.com/jfrog/jfrog-cli-core/v2/common/commands"
	"github.com/jfrog/jfrog-cli-core/v2/plugins/components"
	"github.com/jfrog/jfrog-cli-core/v2/utils/config"
	clientutils "github.com/jfrog/jfrog-client-go/utils"
	"github.com/jfrog/jfrog-client-go/utils/log"

	"strings"

	"os/exec"
)

const ServerIdFlag = "server-id"

func GetAutosetupCommand() components.Command {
	return components.Command{
		Name:        "autosetup",
        Aliases:     []string{"as"},
		Description: "Automatically setup your local package manager to work with a remote Artifactory repo.",
		Flags:       getFlags(),
		Action: func(c *components.Context) error {
			return command(c, "autosetup")
		},
	}
}

func GetTeardownCommand() components.Command {
	return components.Command{
		Name:        "teardown",
		Aliases:     []string{"td"},
		Description: "Automatically remove local package manager connection to remote Artifactory repo.",
		Flags:       getFlags(),
		Action: func(c *components.Context) error {
			return command(c, "teardown")
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


func command(c *components.Context, subcommand string) error {
	var args = c.Arguments

	details, err := getRtDetails(c)
	if err != nil {
		return err
	}

	args = append(
		[]string{
			"commands/autosetup.py",
			subcommand,
			"--username",
			details.User,
			"--password",
			details.Password,
			"--server-url",
			details.Url,
		},
		args...,
	)

	out, err := exec.Command("python", args...).CombinedOutput()

	if err != nil {
		log.Output("Failed to run the Python autosetup script. Stdout/stderr:")
		log.Output(fmt.Sprintf("%s", out))
		log.Output(fmt.Sprintf("%s", err))

		if strings.Contains(fmt.Sprint(err), "executable file not found in") {
			print("Python must be installed to use Python plugins. Please install Python 3 with your operating " +
				   "system's package manager. See https://www.python.org/downloads/")
			return nil
		}
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
