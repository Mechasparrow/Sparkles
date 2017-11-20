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

  connect() {
    let that = this;
    var connection_promise = new Promise(function (resolve, reject) {

      if (that.connection_type == "wallet"){
        that.socket = new WebSocket(endpoint + "/wallet");
      }else {
        that.socket = null
      }

      resolve(that.socket)

    })

    return connection_promise;

  }

  disconnect() {

    this.socket.close()
    this.socket = null;
    return this.socket;

  }


}
