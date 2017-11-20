import { Component, OnInit } from '@angular/core';

//Import the websocket comm
import {SparkleComm} from '../../lib/server-comm';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  public connected:boolean = false

  public wallet_comm:SparkleComm = null;

  constructor() {
    this.wallet_comm = new SparkleComm("wallet")

    let that = this;

    this.wallet_comm.connection_promise.then (function (connection) {
      if (connection != null) {
        that.connected = true;
      }else {
        that.connected = false;
      }
    })


  }

  ngOnInit() {
  }

  sendTransaction() {

  }

  disconnectWallet() {
    var disconnected_message = this.wallet_comm.disconnect();
    if (disconnected_message == null) {
      this.connected = false
    }else {
      return
    }
  }

}
