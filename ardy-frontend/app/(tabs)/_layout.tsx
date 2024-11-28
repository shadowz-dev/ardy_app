import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { NavigationContainer } from '@react-navigation/native';
import { useSession } from '../../components/AuthContext';

// Screen Components
import HomeScreen from './index';
import LoginScreen from './login';
import QuotationsScreen from './quotations';
import ProjectsScreen from './projects';
import ProfileScreen from './profile';

// Create the Tab Navigator
const Tab = createBottomTabNavigator();

export default function TabLayout() {
    const { session, userType } = useSession();
  
    console.log("Auth state:", { session, userType });
  
    const getTabs = () => {
      if (!session) {
        return (
          <>
            <Tab.Screen
              name="Home"
              component={HomeScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'home-sharp' : 'home-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
            <Tab.Screen
              name="Login"
              component={LoginScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'log-in-sharp' : 'log-in-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
          </>
        );
      }
  
      if (userType === 'Customer') {
        return (
          <>
            <Tab.Screen
              name="Home"
              component={HomeScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'home-sharp' : 'home-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
            <Tab.Screen
              name="Quotations"
              component={QuotationsScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'document-sharp' : 'document-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
            <Tab.Screen
              name="Projects"
              component={ProjectsScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'hammer-sharp' : 'hammer-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
            <Tab.Screen
              name="Profile"
              component={ProfileScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'person-circle-sharp' : 'person-circle-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
          </>
        );
      }
  
      if (userType === 'ServiceProvider') {
        return (
          <>
            <Tab.Screen
              name="Home"
              component={HomeScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'home-sharp' : 'home-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
            <Tab.Screen
              name="Projects"
              component={ProjectsScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'hammer-sharp' : 'hammer-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
            <Tab.Screen
              name="Profile"
              component={ProfileScreen}
              options={{
                tabBarIcon: ({ focused, color }) => (
                  <Ionicons
                    name={focused ? 'person-circle-sharp' : 'person-circle-outline'}
                    color={color}
                    size={24}
                  />
                ),
              }}
            />
          </>
        );
      }
  
      return null;
    };
  
    return (
      <Tab.Navigator
        screenOptions={{
          tabBarActiveTintColor: '#7bd3ce',
          headerStyle: {
            backgroundColor: '#2d363b',
          },
          headerTintColor: '#fff',
          tabBarStyle: {
            backgroundColor: '#2d363b',
          },
        }}
      >
        {getTabs()}
      </Tab.Navigator>
    );
  }