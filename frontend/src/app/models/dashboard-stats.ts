export interface DashboardStats {
  companies_total: number;
  applications_total: number;

  by_status: {
    PLANNED: number;
    APPLIED: number;
    INTERVIEW: number;
    ACCEPTED: number;
    REJECTED: number;
  };

  overdue_follow_ups: number;
}
