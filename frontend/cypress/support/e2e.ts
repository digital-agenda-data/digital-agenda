import "./commands";
import "cypress-wait-until";

import verifyDownloads from "cy-verify-downloads";

verifyDownloads.addCustomCommand();
