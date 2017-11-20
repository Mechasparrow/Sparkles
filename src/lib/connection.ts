

export class Connection {

  private const base_message:any = {
    "message_type": "connection"
    "connected": ""
  }

  static connect_message() {
    return base_message;
  }

  static disconnect_message() {
    return base_message;
  }



}
