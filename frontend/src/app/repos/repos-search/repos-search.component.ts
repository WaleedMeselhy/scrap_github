import { Component, OnInit } from "@angular/core";
import { ReposService } from "../repos-service.service";
import { NgForm } from "@angular/forms";
import { Router } from "@angular/router";

@Component({
  selector: "app-repos-search",
  templateUrl: "./repos-search.component.html",
  styleUrls: ["./repos-search.component.css"]
})
export class ReposSearchComponent implements OnInit {
  constructor(private reposService: ReposService, private router: Router) {}

  ngOnInit() {}
  title = "git-repos-analyzer";
  repos = [];
  on_search(form: NgForm) {
    let names = form.value.names;
    let stars = form.value.stars;
    let forked = form.value.forked;
    let repos_names = [];
    for (let i = 0; i < names.length; i++) {
      repos_names.push(names[i].value);
    }
    this.reposService
      .fetchRepos(repos_names, stars, forked)
      .subscribe(response => {
        this.router.navigate(["/repos"], {
          queryParams: {
            repos_names: repos_names,
            stars: stars,
            forked: forked
          }
        });
      });
  }
  onClick(i) {
    console.log("test");
    console.log(i);
  }
}
