import { Component, OnInit, Input } from "@angular/core";
import { ActivatedRoute, Router, Params } from "@angular/router";
import { ReposService } from "../repos-service.service";

@Component({
  selector: "app-repo-details",
  templateUrl: "./repo-details.component.html",
  styleUrls: ["./repo-details.component.css"]
})
export class RepoDetailsComponent implements OnInit {
  repo;
  id: number;
  constructor(
    private repoService: ReposService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.route.params.subscribe((params: Params) => {
      this.id = +params["id"];
      this.repo = this.repoService.getRepo(this.id);
    });
  }
  onClick() {
    console.log(this.repoService.params);

    this.router.navigate(["/repos"], {
      relativeTo: this.route,
      queryParams: {
        repos_names: this.repoService.params["repos_names"],
        stars: this.repoService.params["stars"],
        forked: this.repoService.params["forked"]
      }
    });
  }
}
