import { Component, OnInit } from '@angular/core';

//Sparkle Communication
import {SparkleComm} from '../../lib/server-comm';

//Import services
import {ServercommService} from '../servercomm.service';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrls: ['./transaction.component.css']
})
export class TransactionComponent implements OnInit {

  sparkle_comm: SparkleComm = undefined;

  constructor(private comm_service: ServercommService) {
    this.sparkle_comm = comm_service.get_sparkle_comm();

    console.log(this.sparkle_comm);

  }

  ngOnInit() {
  }

}
