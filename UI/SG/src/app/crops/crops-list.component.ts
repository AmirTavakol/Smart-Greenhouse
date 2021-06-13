
import { Component, OnInit } from '@angular/core';
import { ICrops } from './crops';
import { CropsService } from '../crops/crop-list-service.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
    //selector: 'pm-crops',
    templateUrl: './crops-list.component.html',
    styleUrls: ['./crop-list.component.css']
})

export class CropsListComponent implements OnInit {
    
    pageTitle: string = 'Crops List';
    imageWidth: number = 70;
    imageMargin: number = 2;
    showImage: boolean = true;
    showDetails: boolean = false;

    private _listFilter: string = '';
    private isAutheticated : boolean = false;
    private roles : string[] = [];
    dataLoaded : boolean = false;
    constructor(private cropsService: CropsService, private router: Router, private route: ActivatedRoute) {}

    get listFilter(): string {
        return this._listFilter;
    }
    set listFilter(value: string) {
        if(value != "" || value != null){
            this._listFilter = value;
            console.log('In setter: ', value);
            this.filteredCrops = this.performFilter(value);
        }
    }


    filteredCrops: ICrops[] = [];
     
    crops : ICrops[] = [];


    performFilter(filterBy: string): ICrops[] {
        filterBy = filterBy.toLocaleLowerCase();
        if(filterBy!=''){
            return this.crops.filter((crops: ICrops) =>
            crops.cropName.toLocaleLowerCase().includes(filterBy));
        }
        else{
            return this.crops;
        }
        
    }

    toggleImage(): void {
        this.showDetails = !this.showDetails;
    
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
            var element = document.getElementById("overlay2");
            if(typeof(element)!= undefined && typeof(element)!= null && element){
                element.style.display = "block";
            }
            this.cropsService.getCropsData().subscribe(
                {
                    next: cropsData => {this.crops = cropsData as ICrops[]
                        this.filteredCrops = cropsData as ICrops[];
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


