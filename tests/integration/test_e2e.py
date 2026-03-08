from unittest import mock
from typer.testing import CliRunner
from nova.cli import app

runner = CliRunner()


def test_cli_run_starts_polling(mock_env):
    """
    Test that the CLI `run` command properly initializes the DB and
    calls the synchronous `run_polling` method on the bot Application,
    without encountering asyncio event loop RuntimeErrors.
    """
    with (
        mock.patch("nova.cli.init_db") as mock_init_db,
        mock.patch("nova.bot.platform.Application.builder") as mock_builder,
    ):

        # Setup mock application
        mock_app_instance = mock.MagicMock()
        mock_builder.return_value.token.return_value.build.return_value = (
            mock_app_instance
        )

        # Run the command
        result = runner.invoke(app, ["--log-level", "DEBUG"])

        # Verify it ran without errors
        assert (
            result.exit_code == 0
        ), f"Command failed: {result.output} {result.exception}"

        # Verify DB initialization was called
        mock_init_db.assert_called_once()

        # Verify the bot application was built and run_polling was called
        mock_builder.assert_called_once()
        mock_app_instance.run_polling.assert_called_once()
