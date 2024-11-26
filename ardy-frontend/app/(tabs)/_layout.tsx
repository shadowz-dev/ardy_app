import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
    return (
        <Tabs screenOptions={{ tabBarActiveTintColor: '#7bd3ce',
            headerStyle: {
                backgroundColor: '#2d363b',
                elevation: 0,
                shadowOpacity: 0,
            },
            headerShadowVisible: false,
            headerTintColor: '#fff',
            tabBarStyle: {
                backgroundColor: '#2d363b',
                paddingBottom: 5,
                borderTopWidth: 0,
                shadowColor: 'rgba(0,0,0,0.05)',
                shadowOffset: { width: 0, height: 1 },
                shadowOpacity: 0.8,
                shadowRadius: 2,
                elevation: 5,
            },
        }}>
            <Tabs.Screen name="index" options={{
                title: "Home", 
                tabBarIcon:({ focused, color }) => (
                <Ionicons name={focused ? 'home-sharp' : 'home-outline'} color={color} size={24}/>
                    ),
                }}
                />
            <Tabs.Screen name="about" options={{
                title: "About",
                tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'information-circle-sharp' : 'information-circle-outline'} color={color} size={24}/>

                ),
            }}
            />
        </Tabs>
    );
}