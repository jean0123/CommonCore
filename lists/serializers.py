from core.core_file import CoreSerializer
from users.serializers import UserSerializerShort
from .models import ListItem, ListType, State, Notification


class ListTypeSerializer(CoreSerializer):
    class Meta:
        model = ListType
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        language = self.context.get('language', 'es')
        representation['name'] = representation['name_' + language] if language != 'es' else representation['name']
        representation['description'] = representation['description_' + language] if language != 'es' else representation['description']
        representation['parent'] = ListTypeSerializer(instance.parent).data if instance.parent != None else None
        return representation
    
class ListItemSerializer(CoreSerializer):
    class Meta:
        model = ListItem
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        language = self.context.get('language', 'es')
        representation['name'] = representation['name_' + language] if language != 'es' else representation['name']
        representation['description'] = representation['description_' + language] if language != 'es' else representation['description']
        representation['code'] = representation['code']
        representation['parent'] = ListItemSerializer(instance.parent).data if instance.parent != None else None
        representation['list_type'] = ListTypeSerializer(instance.list_type).data
        return representation

class StateSerializer(CoreSerializer):
    class Meta:
        model = State
        fields = "__all__"

class NotificationSerializer(CoreSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from_user'] = UserSerializerShort(instance.from_user).data
        representation['to_user'] = UserSerializerShort(instance.to_user).data
        representation['state'] = StateSerializer(instance.state).data
        return representation