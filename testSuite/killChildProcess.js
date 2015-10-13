module.exports = function(childProcess) {
  childProcess.kill();
  childProcess.kill("SIGINT");
  childProcess.kill("SIGTERM");
  childProcess.kill("SIGHUP");
};
