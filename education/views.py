from rest_framework import viewsets, generics

from education.models import Course, Lesson
from education.paginators import EducationPaginator
from education.permissions import EducationItemAccess
from education.serializers import CourseSerializer, LessonSerializer
from education.tasks import send_mails_about_update


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [EducationItemAccess]
    pagination_class = EducationPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Course.objects.all()
        if not self.request.user.groups.filter(name='moderator_group').exists():
            queryset = queryset.filter(owner=self.request.user).all()

        return queryset

    def perform_update(self, serializer):
        send_mails_about_update.delay(self.get_object().pk, 'Course')
        serializer.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [EducationItemAccess]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [EducationItemAccess]
    pagination_class = EducationPaginator

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if not self.request.user.groups.filter(name='moderator_group').exists():
            queryset = queryset.filter(owner=self.request.user).all()

        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [EducationItemAccess]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [EducationItemAccess]

    def perform_update(self, serializer):
        send_mails_about_update.delay(self.get_object().pk, 'Lesson')
        serializer.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [EducationItemAccess]
