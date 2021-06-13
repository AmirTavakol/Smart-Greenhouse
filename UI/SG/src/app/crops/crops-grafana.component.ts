import { Component, OnInit } from '@angular/core';
import { CropsGrafanaService } from '../crops/crops-grafana-service.service';
import { ICrop } from '../crops/crop';
import {DomSanitizer, SafeUrl} from '@angular/platform-browser';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  //selector: 'app-crops-grafana',
  templateUrl: './crops-grafana.component.html',
  styleUrls: ['./crops-grafana.component.css']
})
export class CropsGrafanaComponent implements OnInit {
    dataLoaded : boolean = false;
    pageTitle: string = 'Grafana Dashboard';
    cropData : any = {};

  constructor(private service: CropsGrafanaService, private sanitizer: DomSanitizer, private router: Router, private route: ActivatedRoute ) { }

  private isAutheticated : boolean = false;
  private roles : string[] = [];
  private cropId : any;

  getURL() : SafeUrl{
      return this.sanitizer.bypassSecurityTrustResourceUrl(this.cropData.grafanaURL);
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
        this.route.paramMap.subscribe(params => { 
          this.cropId = params.get('cropId'); 
        });
        
        var element = document.getElementById("overlay1");
        if(typeof(element)!= undefined && typeof(element)!= null && element){
          element.style.display = "block";
        }
        this.service.getCropData(this.cropId).subscribe(
          {
            next: cropData => {this.cropData = cropData as ICrop
              this.dataLoaded = true;
              if(typeof(element)!= undefined && typeof(element)!= null && element){
                element.style.display = "none";
              }  
          },
          error: error => {
              console.error('There was an error!', error);
            }
          }
          );
          }
      else{
          this.router.navigate([`/unauthorized`], { relativeTo: this.route })
      }
  }else{
      this.router.navigate([`/invalid`], { relativeTo: this.route })
  }
    
      
  }

}
