function parseArgs() {
  const argv = yargs(hideBin(process.argv))
    .usage('Usage: $0 <flag-name>')
    .command('$0 <flag-name>', 'Enable a feature flag by default', yargs => {
      yargs.positional('flag-name', {
        describe: 'Name of the feature flag to enable',
        type: 'string',
      });
    })
    .example(
      '$0 validateExhaustiveMemoizationDependencies',
      'Enable the validateExhaustiveMemoizationDependencies flag'
    )
    .help('h')
    .alias('h', 'help')
    .strict()
    .parseSync();

  return argv['flag-name'];
}