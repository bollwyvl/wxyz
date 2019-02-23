import { Application, IPlugin } from "@phosphor/application";
import { Widget } from "@phosphor/widgets";

import { IJupyterWidgetRegistry } from "@jupyter-widgets/base";

import {NAME, VERSION} from '.';
import * as widgetExports from "./widgets";
import * as V from "./version";
import "../style/index.css";

const EXTENSION_ID = `${NAME}:plugin`;

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  autoStart: true,
  activate: (app: Application<Widget>, registry: IJupyterWidgetRegistry) => {
    registry.registerWidget({
      name: NAME,
      version: VERSION,
      exports: widgetExports
    });
  }
};

export default plugin;
