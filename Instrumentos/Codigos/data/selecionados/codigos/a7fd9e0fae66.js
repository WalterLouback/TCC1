class AdsPEMultiTabDrawer136 extends React.Component {
    render() {
      if (this.props.x === 299) {
        return React.createElement(
          'div',
          {className: '_2kev _2kex'},
          React.createElement(
            'div',
            {className: '_5yno'},
            React.createElement(AdsPEEditorTrayTabButton83, {
              x: 197,
              key: 'editor_tray_button',
            }),
            React.createElement(AdsPEInsightsTrayTabButton84, {
              x: 202,
              key: 'insights_tray_button',
            }),
            React.createElement(AdsPENekoDebuggerTrayTabButton85, {
              x: 204,
              key: 'neko_debugger_tray_button',
            })
          ),
          React.createElement(
            'div',
            {className: '_5ynn'},
            React.createElement(AdsPEEditorTrayTabContentContainer135, {
              x: 298,
              key: 'EDITOR_DRAWER',
            }),
            null
          )
        );
      }
    }
  }