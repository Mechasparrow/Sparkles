import { Injectable } from '@angular/core';

import {SparkleComm} from '../lib/server-comm';

@Injectable()
export class ServercommService {

  sparkle_comm: SparkleComm = null;

  constructor() {
    this.sparkle_comm = new SparkleComm("wallet");
  }

  get_sparkle_comm() {
    return this.sparkle_comm;
  }

  set_sparkle_comm(new_sparkle_comm: SparkleComm) {
    this.sparkle_comm = new_sparkle_comm;
  }

  change_type(type:string) {
    this.sparkle_comm.connection_type = type;
  }

}
