if __name__ ==  "__main__":
  args = [
        'backtesting',
        '--config', 'config.json',
        '--strategy', 'TesteStrategy2',
        '--export', 'none'
    ]

  # Import here to avoid loading backtesting module when it's not used
  from freqtrade.commands import Arguments
  from freqtrade.commands.optimize_commands import setup_optimize_configuration, start_backtesting
  from freqtrade.enums import RunMode
  from freqtrade.optimize.backtesting import Backtesting


  # Change directory
  # Modify this cell to insure that the output shows the correct path.
  # Define all paths relative to the project root shown in the cell output
  import os
  from pathlib import Path
  project_root = "~/Documents/ambiente/projetos/freqtrade"
  i=0
  try:
      os.chdirdir(project_root)
      assert Path('LICENSE').is_file()
  except:
      while i<4 and (not Path('LICENSE').is_file()):
          os.chdir(Path(Path.cwd(), '../'))
          i+=1
      project_root = Path.cwd()


  # Initialize configuration
  pargs = Arguments(args).get_parsed_arg()
  config = setup_optimize_configuration(pargs, RunMode.BACKTEST)
  # Initialize backtesting object
  backtesting = Backtesting(config)
  backtesting.start()
  backtesting.results