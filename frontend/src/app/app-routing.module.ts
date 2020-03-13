import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { ReposSearchComponent } from "./repos/repos-search/repos-search.component";
import { RepoDetailsComponent } from "./repos/repo-details/repo-details.component";
import { ReposComponent } from "./repos/repos.component";
import { ScrapyJobsComponent } from './scrapy-jobs/scrapy-jobs.component';
const appRoutes: Routes = [
  { path: "", redirectTo: "/datacollection", pathMatch: "full" },
  {
    path: "datacollection",
    component: ScrapyJobsComponent
  },
  {
    path: "repos",
    component: ReposComponent,
    children: [{ path: ":id", component: RepoDetailsComponent }]
  },
  { path: "search", component: ReposSearchComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
