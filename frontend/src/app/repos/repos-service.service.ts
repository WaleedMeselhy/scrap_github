import { Injectable } from "@angular/core";
import { Subject, Observable } from "rxjs";
import { HttpParams, HttpClient } from "@angular/common/http";
import { tap } from "rxjs/operators";
@Injectable({
  providedIn: "root"
})
export class ReposService {
  constructor(private http: HttpClient) {}
  repoChanged = new Subject<any[]>();
  repos = [];
  params = {};
  fetchRepos(names, stars, forked) {
    let searchParams = new HttpParams();
    searchParams = searchParams.append("deps", names);
    this.params["repos_names"] = names;
    if (stars > 0) {
      searchParams = searchParams.append("stars", stars);
      this.params["stars"] = stars;
    }
    if (forked > 0) {
      searchParams = searchParams.append("forked", forked);
      this.params["forked"] = forked;
    }
   
    return this.http
      .get<any[]>("http://localhost:5000/repo/", { params: searchParams })
      .pipe(
        tap(repos => {
          this.repoChanged.next(repos);
          this.repos = repos;
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
}
