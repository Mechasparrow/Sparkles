

export class Connection {

  static get_connection_message(connect:boolean) {
    const connect_message:any = {
      "message_type": "connection",
      "connection": connect
    }

    return connect_message

  }

  static connect_message(stringify) {
    var connect_msg:any = Connection.get_connection_message(true)

    if (stringify == true) {
      return <string>JSON.stringify(connect_msg)
    }

    return <any>connect_msg;



  }

  static disconnect_message(stringify) {
    var connect_msg:any = Connection.get_connection_message(false)

    if (stringify == true) {
      return <string>JSON.stringify(connect_msg)
    }

    return <any>connect_msg;
  }



}
