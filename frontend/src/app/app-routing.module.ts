import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { ReposSearchComponent } from "./repos/repos-search/repos-search.component";
import { RepoDetailsComponent } from "./repos/repo-details/repo-details.component";
import { ReposComponent } from "./repos/repos.component";
const appRoutes: Routes = [
  { path: "", redirectTo: "/repos", pathMatch: "full" },
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
export class AppRoutingModule {}
