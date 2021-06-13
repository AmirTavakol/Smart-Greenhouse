import { Component, OnInit } from '@angular/core';
import { CropsGrafanaService } from '../crops/crops-grafana-service.service';
import { ICrop } from '../crops/crop';
import { Router, ActivatedRoute } from '@angular/router';
import {ManualActionServiceService} from './manual-action-service.service'

@Component({
  selector: 'app-action',
  templateUrl: './action.component.html',
  styleUrls: ['./action.component.css']
})
export class ActionComponent implements OnInit {

  constructor(private service: CropsGrafanaService, private router: Router, private route: ActivatedRoute,
              private manualService : ManualActionServiceService) { }
  cropData : any = {}
  private isAutheticated : boolean = false;
  private roles : string[] = [];
  
  manualTrigger(): void {
    let re = "false";
    this.manualService.manualTriggerOn(this.cropData.id).subscribe({
        next: result => {
          re = result;
          window.localStorage.clear();
          window.location.reload();
        },
      error: error => {
          console.error('There was an error!', error);
        }
      })
  }

  ngOnInit(): void {
    if(window.sessionStorage.getItem('user')){
      let data = window.sessionStorage.getItem('user');
      if(typeof(data) != undefined && typeof(data)!= null && data){
          let userData = JSON.parse(data);
          this.isAutheticated = userData.isAuthenticated;
          this.roles = userData.roles;     
      }
  }
  if(this.isAutheticated){
      if(this.roles.includes('farmer')){
          if(typeof(history.state.data) != undefined && history.state.data){
            this.cropData = history.state.data;
            window.localStorage.setItem('cropData',JSON.stringify(this.cropData));
          }
       else if(window.localStorage.getItem('cropData')){
           var result = window.localStorage.getItem('cropData');
           if(result && typeof(result) != undefined && typeof(result)!= null){
             this.cropData = JSON.parse(result);
           }
          }
       else{
         this.service.getCropData(this.cropData.id).subscribe(cropData => {this.cropData = cropData as ICrop});
          }
      }
      else{
          this.router.navigate([`/unauthorized`], { relativeTo: this.route })
        }
      }else{
      this.router.navigate([`/invalid`], { relativeTo: this.route })
      }
    
  }

}