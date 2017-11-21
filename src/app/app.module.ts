import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule} from '@angular/forms';

import { AppComponent } from './app.component';

import {RouterModule, Router, Routes} from '@angular/router';
import { HomeComponent} from './home/home.component';
import { TransactionComponent } from './transaction/transaction.component';

import { ServercommService } from './servercomm.service';

const appRoutes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'transaction', component: TransactionComponent}
]

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    TransactionComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(
      appRoutes,
      {enableTracing: true}
    ),
    FormsModule
  ],
  providers: [ServercommService],
  bootstrap: [AppComponent]
})
export class AppModule { }
