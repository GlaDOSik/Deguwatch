const Vial = {
    component: {
        modal: {
            open(modalId) {
                const modal = document.getElementById(modalId);
                modal.style.display = "block";
            },
            close(modalId) {
                const modal = document.getElementById(modalId);
                modal.style.display = "none";
            }
        },
        store: {
            put(componentId, key, value) {
                if (componentId in Vial.component.store.data) {
                    Vial.component.store.data[componentId][key] = value;
                } else {
                    let compData = {};
                    compData[key] = value;
                    Vial.component.store.data[componentId] = compData;
                }
            },
            get(componentId, key) {
                return Vial.component.store.data[componentId][key];
            },
            data: {}
        }
    },
    callback: {
        // callbackName - class name of WebCallback
        // webComponentData - object where id is component id and value WebComponentData class name to be loaded as input from frontend
        // requestedComponentIds - list of component ids to be rerendered
        nop(callbackName, webComponentData, requestedComponentIds, afterRender) {
            let basePayload = Vial.callback.basePayload(callbackName, webComponentData);
            basePayload["requested-components"] = requestedComponentIds;
            Vial.utils.postJson("/api/vial/callback", basePayload)
            .then(response => {
                if (!response.ok) {
                  console.error("NOP callback error: ", error);
                  throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                Vial.utils.handleWebCallbackResponse(data);
                if (afterRender != null) {
                    afterRender();
                }
            })
            .catch(error => {
                console.error("NOP callback error: ", error);
            });
        },
        basePayload(callbackName, webComponentData) {
            var callback_payload = {"callback-name": callbackName, "web-component-data": {}};

            for (const [id, methodName] of Object.entries(webComponentData)) {
                const funcName = methodName.charAt(0).toLowerCase() + methodName.slice(1);
                const func = window[funcName];

                if (typeof func === "function") {
                    callback_payload["web-component-data"][id + " - " + methodName] = func(id);
                } else {
                    console.warn(`WCD function ${funcName} not found`);
                }
            }
            return callback_payload;
        }
    },
    utils: {
         decodeBase64(base64) {
            const text = atob(base64);
            const length = text.length;
            const bytes = new Uint8Array(length);
            for (let i = 0; i < length; i++) {
                bytes[i] = text.charCodeAt(i);
            }
            const decoder = new TextDecoder(); // default is utf-8
            return decoder.decode(bytes);
        },
        handleWebCallbackResponse(data) {
            if (data.isRedirect === true) {
                window.location.replace(data.redirectUrl);
            } else {
                for (const [key, value] of Object.entries(data.components)) {
                    const htmlComponent = document.getElementById(key);
                    htmlComponent.innerHTML = Vial.utils.decodeBase64(value);
                }
                return data.data;
            }
        },
        postJson(path) {
            postJson(path, null);
        },
        postJson(path, payload) {
            return fetch(Vial.component.store.get('global', 'server-url') + path, {
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                method: "POST",
                body: JSON.stringify(payload)
            })
        }
    }
};