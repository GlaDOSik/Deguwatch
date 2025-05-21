function createCameraShot() {
    let componentData = createEditCameraShotWebComponentData();
    Vial.utils.postJson("/api/entity/camera-shot", componentData);
}

function openLivestream(cameraShotId) {
    window.location.href = "/shot/" + cameraShotId;
}

function openImageView(imageId) {
    window.location.href = "/shot/image/" + imageId;
}

function openDashboard() {
    window.location.href = "/dashboard/";
}