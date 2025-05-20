function createEditCameraShotWebComponentData() {
    const shotName = document.getElementById("name").value;
    const deviceId = document.getElementById("deviceId").value;
    const saveFrequency = document.getElementById("saveFrequency").value;
    const putTimestamp = document.getElementById("timestamp").checked;
    return {"shot-name": shotName, "device-id": deviceId, "save-frequency": saveFrequency, "put-timestamp": putTimestamp};
}