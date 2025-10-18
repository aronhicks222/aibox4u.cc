import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Heart } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { mockTools } from '../mockData';
import { Link } from 'react-router-dom';

const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [favorites] = useState(['1', '3', '6']); // Mock favorite IDs

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
    } else {
      setUser(JSON.parse(userData));
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/');
  };

  const favoriteTools = mockTools.filter(tool => favorites.includes(tool.id));

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-br from-purple-600 to-pink-500 text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <Button variant="ghost" onClick={() => navigate('/')} className="text-white hover:bg-white/20 mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
          <div className="flex items-center gap-4">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center">
              <User className="w-10 h-10 text-purple-600" />
            </div>
            <div>
              <h1 className="text-4xl font-bold">{user.name}</h1>
              <p className="text-lg opacity-90">{user.email}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="md:col-span-1">
            <Card>
              <CardContent className="p-6 space-y-2">
                <Button variant="ghost" className="w-full justify-start">
                  <Heart className="w-4 h-4 mr-2" />
                  Favorites ({favoriteTools.length})
                </Button>
                <Button variant="ghost" className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50" onClick={handleLogout}>
                  Logout
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="md:col-span-3">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="w-5 h-5" />
                  Your Favorite Tools
                </CardTitle>
              </CardHeader>
              <CardContent>
                {favoriteTools.length === 0 ? (
                  <div className="text-center py-12">
                    <Heart className="w-12 h-12 mx-auto text-gray-300 mb-4" />
                    <p className="text-gray-500">You haven't saved any tools yet.</p>
                    <Button className="mt-4" onClick={() => navigate('/')}>Browse Tools</Button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {favoriteTools.map(tool => (
                      <Card key={tool.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                        <Link to={`/tool/${tool.id}`}>
                          <img src={tool.image} alt={tool.name} className="w-full h-40 object-cover" />
                        </Link>
                        <CardContent className="p-4">
                          <Link to={`/tool/${tool.id}`}>
                            <h3 className="text-lg font-bold mb-2 hover:text-purple-600">{tool.name}</h3>
                          </Link>
                          <Badge className="bg-teal-500 text-white mb-2">{tool.category}</Badge>
                          <p className="text-gray-600 text-sm line-clamp-2">{tool.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
