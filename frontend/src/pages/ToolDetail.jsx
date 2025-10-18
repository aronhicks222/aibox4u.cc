import React from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, ExternalLink, Heart } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Card, CardContent } from '../components/ui/card';
import { mockTools } from '../mockData';

const ToolDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const tool = mockTools.find(t => t.id === id);

  if (!tool) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Tool not found</h2>
          <Button onClick={() => navigate('/')}>Back to Home</Button>
        </div>
      </div>
    );
  }

  const relatedTools = mockTools.filter(t => t.category === tool.category && t.id !== tool.id).slice(0, 3);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <Button variant="ghost" onClick={() => navigate('/')} className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Directory
          </Button>
          
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-2">{tool.name}</h1>
              <p className="text-xl text-gray-600 mb-4">{tool.description}</p>
              
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge className="bg-teal-500 text-white text-sm px-3 py-1">
                  {tool.category}
                </Badge>
                <Badge className="bg-gray-200 text-gray-800 text-sm px-3 py-1">
                  {tool.pricing}
                </Badge>
              </div>
              
              <div className="flex gap-3">
                <a href={tool.url} target="_blank" rel="noopener noreferrer">
                  <Button className="bg-pink-600 hover:bg-pink-700 text-white">
                    Visit Website <ExternalLink className="w-4 h-4 ml-2" />
                  </Button>
                </a>
                <Button variant="outline" className="border-pink-600 text-pink-600 hover:bg-pink-50">
                  <Heart className="w-4 h-4 mr-2" />
                  Save to Favorites
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2">
            <Card className="mb-6">
              <CardContent className="p-6">
                <img 
                  src={tool.image} 
                  alt={tool.name}
                  className="w-full h-96 object-cover rounded-lg mb-6"
                />
                
                <h2 className="text-2xl font-bold mb-4">About {tool.name}</h2>
                <p className="text-gray-700 text-lg leading-relaxed mb-6">
                  {tool.longDescription}
                </p>
                
                <div className="border-t pt-6">
                  <h3 className="text-xl font-bold mb-3">Key Features</h3>
                  <ul className="list-disc list-inside space-y-2 text-gray-700">
                    <li>AI-powered automation</li>
                    <li>Easy to use interface</li>
                    <li>Fast and reliable</li>
                    <li>Regular updates and improvements</li>
                    <li>Great customer support</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Sidebar */}
          <div className="lg:col-span-1">
            <Card className="mb-6">
              <CardContent className="p-6">
                <h3 className="text-xl font-bold mb-4">Tags</h3>
                <div className="flex flex-wrap gap-2">
                  {tool.tags.map((tag, idx) => (
                    <Badge key={idx} variant="outline" className="bg-green-100 text-green-800 border-green-300">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <h3 className="text-xl font-bold mb-4">Pricing</h3>
                <div className="bg-purple-50 rounded-lg p-4 text-center">
                  <p className="text-3xl font-bold text-purple-600 mb-2">{tool.pricing}</p>
                  <p className="text-gray-600 text-sm">Visit website for detailed pricing</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Related Tools */}
        {relatedTools.length > 0 && (
          <div className="mt-12">
            <h2 className="text-3xl font-bold mb-6">Related Tools in {tool.category}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {relatedTools.map(relatedTool => (
                <Card key={relatedTool.id} className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                  <Link to={`/tool/${relatedTool.id}`}>
                    <img 
                      src={relatedTool.image} 
                      alt={relatedTool.name}
                      className="w-full h-48 object-cover"
                    />
                  </Link>
                  <CardContent className="p-4">
                    <Link to={`/tool/${relatedTool.id}`}>
                      <h3 className="text-lg font-bold mb-2 hover:text-purple-600">{relatedTool.name}</h3>
                    </Link>
                    <Badge className="bg-teal-500 text-white text-xs mb-2">
                      {relatedTool.category}
                    </Badge>
                    <p className="text-gray-600 text-sm line-clamp-2">{relatedTool.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ToolDetail;
