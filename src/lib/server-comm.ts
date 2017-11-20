import {endpoint} from './server-endpoint';
import {Connection} from './connection';

export class SparkleComm {

  public socket:any = null;
  public connection_type:string = "none"
  public connection_promise:any = undefined;

  constructor (type:string) {

    this.connection_type = type;
    this.connection_promise = this.connect();

  }

  static display_endpoint() {
    console.log(endpoint)
  }

  getConnection() {
    return this.socket;
  }

  on_open (event, socket) {
    var connect_message = Connection.connect_message(true);
    console.log(connect_message)
    socket.send(connect_message);
  }

  connect() {
    let that = this;
    var connection_promise = new Promise(function (resolve, reject) {

      if (that.connection_type == "wallet"){
        that.socket = new WebSocket(endpoint + "/wallet");
        that.socket.addEventListener('open', function (event) {
          that.on_open(event, that.socket);
        });
      }else {
        that.socket = null
      }

      resolve(that.socket)

    })

    return connection_promise;

  }

  disconnect() {

    this.socket.send(Connection.disconnect_message(true));
    this.socket.close()
    this.socket = null;
    return this.socket;

  }


}
