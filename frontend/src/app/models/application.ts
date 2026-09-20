export interface Application {
  id: number;
  company: number;
  position: string;
  status: string;
  status_display: string;
  application_date: string | null;
  job_url: string;
  contact_person: string;
  contact_email: string;
  next_action: string;
  next_action_date: string | null;
  notes: string;
  created_at: string;
  updated_at: string;
}
