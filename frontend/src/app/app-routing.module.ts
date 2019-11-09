import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { ReposListComponent } from "./repos/repos-list/repos-list.component";
import { ReposSearchComponent } from "./repos/repos-search/repos-search.component";
const appRoutes: Routes = [
  { path: "", redirectTo: "/repos", pathMatch: "full" },
  { path: "repos", component: ReposListComponent },
  { path: "search", component: ReposSearchComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
