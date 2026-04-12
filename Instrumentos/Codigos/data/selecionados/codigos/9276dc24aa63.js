function getDefaultsForModernBrowsers(features) {
  const combined = {
    presets: [],
    plugins: [getReifyPlugin(features)]
  };

  const compileModulesOnly = features && features.compileModulesOnly;
  if (! compileModulesOnly) {
    combined.presets.push(babelPresetMeteorModern.getPreset);

    const rt = getRuntimeTransform(features);
    if (rt) {
      combined.plugins.push(rt);
    }

    maybeAddReactPlugins(features, combined);
  }

  return finish(features, [combined]);
}