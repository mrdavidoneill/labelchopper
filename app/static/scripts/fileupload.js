function initDropZone(user, progressDiv, progressContainerDiv) {
  Dropzone.options.fileupload = {
    parallelUploads: 1,
    timeout: 0,
    dictDefaultMessage: "Drop files here or click to browse",
    init: function () {
      let socket;

      this.on("processing", () => {
        socket = createProgressSocket(socket, user, progressDiv);
        showProgress(progressContainerDiv);
      });

      this.on("complete", () => {
        closeProgressSocket(socket);
        hideProgress(progressContainerDiv);
      });

      this.on("success", function (file, serverResponse) {
        let url = window.location.pathname + "convert/";
        url = url + serverResponse;
        window.location = url;
      });
    },
  };
}

function createProgressSocket(socket, user, progressDiv) {
  socket = io("/progress");

  socket.emit("start", user);

  socket.on("progress", function (value) {
    updateProgress(progressDiv, value);
  });

  return socket;
}

function closeProgressSocket(socket) {
  socket.emit("stop");
}

function updateProgress(progressId, value) {
  document.querySelector(progressId).style.width = `${value * 100}%`;
}

function showProgress(progressContainerDiv) {
  document.querySelector(progressContainerDiv).style.display = "flex";
}

function hideProgress(progressContainerDiv) {
  document.querySelector(progressContainerDiv).style.display = "none";
}
