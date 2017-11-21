import { Component, OnInit } from '@angular/core';

//Import the websocket comm
import {SparkleComm} from '../../lib/server-comm';

//Import services
import {ServercommService} from '../servercomm.service';

//Routing
import {Router, ActivatedRoute, ParamMap} from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  public connected:boolean = false

  public wallet_comm:SparkleComm = null;

  constructor(private comm_service: ServercommService,
    private route: ActivatedRoute,
    private router: Router
  ) {
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
    this.comm_service.set_sparkle_comm(this.wallet_comm);
    this.router.navigate(['/transaction']);
  }

  disconnectWallet() {
    var disconnected_message = this.wallet_comm.disconnect();
    if (disconnected_message == null) {
      this.connected = false
    }else {
      return
    }
  }

  connectWallet() {
    let that = this;
    var connection_promise = that.wallet_comm.connect();

    connection_promise.then (function (connection) {
      if (connection != null) {
        that.connected = true;
      }else {
        that.connected = false;
      }
    })

  }

}
