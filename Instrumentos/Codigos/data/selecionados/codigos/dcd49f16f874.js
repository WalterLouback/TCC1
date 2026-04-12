function ensureCacheDir(cacheDir) {
  cacheDir = path.resolve(
    cacheDir ||
    process.env.BABEL_CACHE_DIR ||
    path.join(
      process.env.HOME || process.env.USERPROFILE || __dirname,
      ".babel-cache"
    )
  );

  try {
    util.mkdirp(cacheDir);
  } catch (error) {
    if (error.code !== "EEXIST") {
      throw error;
    }
  }

  return cacheDir;
}