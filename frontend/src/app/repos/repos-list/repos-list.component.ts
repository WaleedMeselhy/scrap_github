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
    this.route.queryParams.subscribe((params: Params) => {
      this.repoService
        .fetchRepos(params.repos_names, params.stars, params.forked)
        .subscribe();
    });

    this.subscription = this.repoService.repoChanged.subscribe(
      (repos: any[]) => {
        this.repos = repos;
      }
    );
    this.repos = this.repoService.getRepos();
  }
}
