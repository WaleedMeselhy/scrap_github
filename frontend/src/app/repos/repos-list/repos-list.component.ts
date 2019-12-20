import { Component, OnInit, OnDestroy } from "@angular/core";
import { Subscription } from "rxjs";
import { ReposService } from "../repos-service.service";
import { ActivatedRoute, Params } from "@angular/router";

@Component({
  selector: "app-repos-list",
  templateUrl: "./repos-list.component.html",
  styleUrls: ["./repos-list.component.css"]
})
export class ReposListComponent implements OnInit, OnDestroy {
  subscription: Subscription;
  repos: any[];
  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
  constructor(
    private repoService: ReposService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    let repos_names = this.route.snapshot.queryParams["repos_names"];
    if (!(repos_names instanceof Array)) {
      repos_names = [repos_names];
    }
    let stars = this.route.snapshot.queryParams["stars"];
    let forked = this.route.snapshot.queryParams["forked"];
    this.route.queryParams.subscribe((params: Params) => {
      if (this.repoService.checkParamsChange(repos_names, stars, forked)) {
        this.repoService
          .fetchRepos(params.repos_names, params.stars, params.forked)
          .subscribe();
      } else {
        this.repos = this.repoService.repos;
      }
    });

    this.subscription = this.repoService.repoChanged.subscribe(
      (repos: any[]) => {
        this.repos = repos;
      }
    );
    // this.repos = this.repoService.getRepos();
  }
}
