Dropzone.options.fileupload = {
  parallelUploads: 1,
  timeout: 0,
  dictDefaultMessage: "Drop files here or click to browse",
  init: function () {
    this.on("success", function (file, serverResponse) {
      let url = window.location.pathname + "convert/";
      url = url + serverResponse;
      window.location = url;
    });
  },
};
