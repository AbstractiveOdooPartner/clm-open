/** @odoo-module **/
// [PEP-MIJN-ACCOUNT]. NOTE: This entire file is a modified version of project/static/src/project_sharing/project_sharing.js

import { useBus, useService } from '@web/core/utils/hooks';
import { useExternalListener, useLayoutEffect } from "@web/owl2/utils";
import { ActionContainer } from '@web/webclient/actions/action_container';
import { MainComponentsContainer } from "@web/core/main_components_container";
import { useOwnDebugContext } from "@web/core/debug/debug_context";
import { session } from '@web/session';
import { Component, proxy, usePlugin } from "@odoo/owl";
import { ActionManagerPlugin } from "@web/webclient/actions/action_plugin";

export class ContactSharingWebClient extends Component {
    setup() {
        window.parent.document.body.style.margin = "0"; // remove the margin in the parent body
        this.actionService = usePlugin(ActionManagerPlugin);
        this.user = useService("user");
        useOwnDebugContext({ categories: ["default"] });
        this.state = proxy({
            fullscreen: false,
        });
        useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", (mode) => {
            if (mode !== "new") {
                this.state.fullscreen = mode === "fullscreen";
            }
        });
        useLayoutEffect(
            () => {
                this._showView();
            },
            () => []
        );
        useExternalListener(window, "click", this.onGlobalClick, { capture: true });
    }

    async _showView() {
        const { action_name, contact_id, view_id } = session;
        await this.actionService.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "res.partner",
                res_id: contact_id,
                views: [[view_id, "form"]],
                target: "current",
            },
            {
                clearBreadcrumbs: true,
            }
        );
    }

    /**
     * @param {MouseEvent} ev
     */
    onGlobalClick(ev) {
        // When a ctrl-click occurs inside an <a href/> element
        // we let the browser do the default behavior and
        // we do not want any other listener to execute.
        if (
            ev.ctrlKey &&
            ((ev.target instanceof HTMLAnchorElement && ev.target.href) ||
                (ev.target instanceof HTMLElement && ev.target.closest("a[href]:not([href=''])")))
        ) {
            ev.stopImmediatePropagation();
            return;
        }
    }
}

ContactSharingWebClient.props = {};
ContactSharingWebClient.components = { ActionContainer, MainComponentsContainer };
ContactSharingWebClient.template = 'clm_contact_manager.ContactSharingWebClient';
