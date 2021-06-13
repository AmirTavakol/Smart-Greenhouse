import { HttpClientModule } from '@angular/common/http';
import { AuthService } from './login/auth.service';

import { LoginComponent } from './login/login.component';
import { NgStyle } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { CropsListComponent } from './crops/crops-list.component';
import { CropsGrafanaComponent } from './crops/crops-grafana.component';
import { ActionComponent } from './action/action.component';
import {EndrDecrServiceService} from './endr-decr-service.service';
import { InvalidUserComponent } from './login/invalid-user/invalid-user.component';
import { UnauthorizedUserComponent } from './login/unauthorized-user/unauthorized-user.component';
import { LogoutComponent } from './logout/logout.component';

@NgModule({
  declarations: [
    AppComponent,
    CropsListComponent,
    CropsGrafanaComponent,
    LoginComponent,
    ActionComponent,
    InvalidUserComponent,
    UnauthorizedUserComponent,
    LogoutComponent
    
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot([
      { path: 'crops', component: CropsListComponent},
      { path: 'grafana/:cropId', component: CropsGrafanaComponent},
      { path: 'login', component: LoginComponent},
      { path: 'action', component: ActionComponent},
      {path: 'invalid', component :InvalidUserComponent},
      {path: 'unauthorized', component :UnauthorizedUserComponent},
      {path: 'logout', component :LogoutComponent},
      { path: '', redirectTo: 'login', pathMatch: 'full'}
    ])
  ],
  providers: [
    EndrDecrServiceService,AuthService
],
  
  bootstrap: [AppComponent]
})
export class AppModule { }
