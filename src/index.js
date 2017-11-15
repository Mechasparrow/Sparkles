$(document).ready(function () {

  var walletSocket = new WebSocket("ws://localhost:5000/wallet")

  var connect_message = {
        'message_type': 'connection',
        'connection': true
  }

  var disconnect_message = {
    'message_type': 'connection',
    'connection': false
  }

  var connect_message_json = JSON.stringify(connect_message)
  var disconnect_message_json = JSON.stringify(disconnect_message)

  console.log(connect_message_json)

  walletSocket.onopen = function (event) {
    walletSocket.send(connect_message_json)
  }

  $('#disconnect-btn').click(function (event) {
    walletSocket.send(disconnect_message_json)
    walletSocket.close()
  })

})
