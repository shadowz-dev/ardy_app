# core/tests/test_phase_views.py

from ..models import Projects, Phase, CustomerProfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..tests import create_user 
from ..constants import *

class PhaseViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_user(username="phase_cust", user_type="Customer", email="pcust@example.com", phone="+97150...")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        self.sp_user = create_user(username="phase_sp", user_type="Consultant", email="psp@example.com", phone="+97150...")

        self.project = Projects.objects.create(customer=self.customer_profile, title="Project For Phases")

    def test_customer_creates_phase_for_own_project(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:phase-list') # Assumes 'phase-list' from router
        data = {
            "project": self.project.pk,
            "title": "Initial Design Phase",
            "order": 1,
            "service_provider": self.sp_user.pk # Optional: customer might assign SP during phase creation
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Phase.objects.count(), 1)
        self.assertEqual(Phase.objects.first().title, "Initial Design Phase")

    def test_list_phases_for_project_as_customer(self):
        Phase.objects.create(project=self.project, title="P1", order=1, service_provider=self.sp_user)
        Phase.objects.create(project=self.project, title="P2", order=2, service_provider=self.sp_user)
        
        self.client.force_authenticate(user=self.customer_user)
        # URL might be /api/phases/?project_id=<id> or if using nested: /api/projects/<pk>/phases/
        url = reverse('core:phase-list') + f'?project_id={self.project.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Or check paginated response count

    def test_sp_lists_phases_assigned_to_them(self):
        p2 = Projects.objects.create(customer=self.customer_profile, title="Another Project")
        Phase.objects.create(project=self.project, title="P1", order=1, service_provider=self.sp_user)
        Phase.objects.create(project=p2, title="P2A1", order=1) # No SP

        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:phase-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Only sees P1
        self.assertEqual(response.data[0]['title'], "P1")

    def test_complete_phase_action(self):
        phase = Phase.objects.create(project=self.project, title="Completable Phase", order=1, service_provider=self.sp_user)
        self.project.start_project(initial_phase=phase) # Project and Phase are 'In Progress'

        self.client.force_authenticate(user=self.sp_user) # SP completes their phase
        url = reverse('core:phase-complete-phase-action', kwargs={'pk': phase.pk}) # 'phase-complete-phase-action'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        phase.refresh_from_db()
        self.assertEqual(phase.status, STATUS_COMPLETED)