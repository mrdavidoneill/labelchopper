Dropzone.options.fileupload = {
  parallelUploads: 1,
  dictDefaultMessage: "Please log in to use Label Chopper",
  autoProcessQueue: false,
  init: function () {
    this.on("addedfile", function (file) {
      $("#login-modal").modal();
      this.removeFile(file);
    });
  },
};
