import { Injectable } from "@angular/core";
import { Subject, Observable, forkJoin, from } from "rxjs";
import { HttpParams, HttpClient } from "@angular/common/http";
import { tap, mergeMap } from "rxjs/operators";
import { environment } from "../../environments/environment";
@Injectable({
  providedIn: "root"
})
export class ReposService {
  constructor(private http: HttpClient) {}
  repoChanged = new Subject<any[]>();
  repos = [];
  params = {};
  checkParamsChange(names, stars, forked) {
    if (
      this.params["repos_names"] &&
      this.params["repos_names"].length === names.length &&
      this.params["repos_names"].every((value, index) => value === names[index])
    ) {
      if (
        this.params["stars"] === +stars &&
        this.params["forked"] === +forked
      ) {
        return false;
      } else return true;
    } else return true;
  }
  fetchRepos(names, stars, forked) {
    let searchParams = new HttpParams();
    searchParams = searchParams.append("deps", names);
    this.params["repos_names"] = names;
    if (stars > 0) {
      searchParams = searchParams.append("stars", stars);
    }
    this.params["stars"] = stars;
    if (forked > 0) {
      searchParams = searchParams.append("forked", forked);
    }
    this.params["forked"] = forked;
    this.repos = [];
    return this.http
      .get<any[]>(environment.backend_url + "/repo/v2", {
        params: searchParams
      })
      .pipe(
        tap(repos => {
          const requests = from(repos["repos"]).pipe(
            mergeMap(repo =>
              this.http.get<any[]>(environment.backend_url + repo)
            )
          );
          requests.subscribe(
            data => {
              console.log(data);
              this.repos.push(data)
              this.repoChanged.next(this.repos);
              // this.repos = repos;
            }, //process item or push it to array
            err => console.log(err)
          );
        })
      );
  }
  getRepos() {
    return this.repos.slice();
  }
  getRepo(id: number) {
    for (let i = 0; i < this.repos.length; i++) {
      if (this.repos[i].id === id) {
        return this.repos[i];
      }
    }
    return null;
  }
  fetchRepoDeps(repo_id: number) {
    return this.http.get<any[]>(
      environment.backend_url + "/repo/v2/" + repo_id
    );
  }
  fetchRepoDepsDetails(repos: []) {
    let repos_details = [];
    for (let i = 0; i < repos.length; i++) {
      repos_details.push(
        this.http.get<any[]>(environment.backend_url + repos[i])
      );
    }

    return forkJoin(repos_details);
  }
}
