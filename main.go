package main

import (
	"github.com/jfrog/jfrog-cli-core/v2/plugins"
	"github.com/jfrog/jfrog-cli-core/v2/plugins/components"
	"github.com/sveder/jfrog-cli-autosetup/commands"
)

func main() {
	plugins.PluginMain(getApp())
}

func getApp() components.App {
	app := components.App{}
	app.Name = "autosetup"
	app.Description = "Easily and automatically setup and teardown your machine to work with a remote Artifactory repo."
	app.Version = "v1.0.0"
	app.Commands = getCommands()
	return app
}

func getCommands() []components.Command {
	return []components.Command{
		commands.GetAutosetupCommand(),
		commands.GetTeardownCommand(),
	}
}
