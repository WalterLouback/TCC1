class ExtensionData {
  #type
  #path

  constructor(type, path) {
    this.#type = type
    this.#path = path
  }

  static setPath(path) {
    return new ExtensionData('path', path)
  }

  static setArchivePath(path) {
    return new ExtensionData('archivePath', path)
  }

  static setBase64Encoded(value) {
    return new ExtensionData('base64', value)
  }

  asMap() {
    let toReturn = {}
    toReturn['type'] = this.#type

    if (this.#type === 'base64') {
      toReturn['value'] = this.#path
    } else {
      toReturn['path'] = this.#path
    }

    return toReturn
  }
}