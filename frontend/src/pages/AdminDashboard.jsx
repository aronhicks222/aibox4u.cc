import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Edit, Trash2, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { useToast } from '../hooks/use-toast';
import { mockTools, categories } from '../mockData';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [tools, setTools] = useState(mockTools);
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [editingTool, setEditingTool] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    longDescription: '',
    category: '',
    pricing: '',
    url: '',
    image: '',
    tags: '',
    featured: false
  });

  const handleDelete = (id) => {
    if (window.confirm('Are you sure you want to delete this tool?')) {
      setTools(tools.filter(t => t.id !== id));
      toast({
        title: "Tool Deleted",
        description: "The tool has been removed from the directory.",
      });
    }
  };

  const handleEdit = (tool) => {
    setEditingTool(tool);
    setFormData({
      name: tool.name,
      description: tool.description,
      longDescription: tool.longDescription,
      category: tool.category,
      pricing: tool.pricing,
      url: tool.url,
      image: tool.image,
      tags: tool.tags.join(', '),
      featured: tool.featured
    });
    setIsAddDialogOpen(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const tagsArray = formData.tags.split(',').map(t => t.trim());
    
    if (editingTool) {
      setTools(tools.map(t => t.id === editingTool.id ? {
        ...editingTool,
        ...formData,
        tags: tagsArray
      } : t));
      toast({
        title: "Tool Updated",
        description: "The tool has been updated successfully.",
      });
    } else {
      const newTool = {
        id: String(tools.length + 1),
        ...formData,
        tags: tagsArray
      };
      setTools([...tools, newTool]);
      toast({
        title: "Tool Added",
        description: "New tool has been added to the directory.",
      });
    }
    
    setIsAddDialogOpen(false);
    setEditingTool(null);
    setFormData({
      name: '',
      description: '',
      longDescription: '',
      category: '',
      pricing: '',
      url: '',
      image: '',
      tags: '',
      featured: false
    });
  };

  const resetForm = () => {
    setEditingTool(null);
    setFormData({
      name: '',
      description: '',
      longDescription: '',
      category: '',
      pricing: '',
      url: '',
      image: '',
      tags: '',
      featured: false
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-br from-purple-600 to-pink-500 text-white py-8 px-4">
        <div className="max-w-7xl mx-auto">
          <Button variant="ghost" onClick={() => navigate('/')} className="text-white hover:bg-white/20 mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
          <h1 className="text-4xl font-bold">Admin Dashboard</h1>
          <p className="text-lg opacity-90 mt-2">Manage AI Tools Directory</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>All Tools ({tools.length})</CardTitle>
            <Dialog open={isAddDialogOpen} onOpenChange={(open) => {
              setIsAddDialogOpen(open);
              if (!open) resetForm();
            }}>
              <DialogTrigger asChild>
                <Button className="bg-pink-600 hover:bg-pink-700 text-white">
                  <Plus className="w-4 h-4 mr-2" />
                  Add New Tool
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>{editingTool ? 'Edit Tool' : 'Add New Tool'}</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Label>Tool Name</Label>
                    <Input value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} required />
                  </div>
                  <div>
                    <Label>Short Description</Label>
                    <Textarea value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} required rows={2} />
                  </div>
                  <div>
                    <Label>Full Description</Label>
                    <Textarea value={formData.longDescription} onChange={(e) => setFormData({...formData, longDescription: e.target.value})} required rows={3} />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Category</Label>
                      <Select value={formData.category} onValueChange={(value) => setFormData({...formData, category: value})} required>
                        <SelectTrigger>
                          <SelectValue placeholder="Select category" />
                        </SelectTrigger>
                        <SelectContent>
                          {categories.filter(c => c !== 'All').map(cat => (
                            <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label>Pricing</Label>
                      <Select value={formData.pricing} onValueChange={(value) => setFormData({...formData, pricing: value})} required>
                        <SelectTrigger>
                          <SelectValue placeholder="Select pricing" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Free">Free</SelectItem>
                          <SelectItem value="Paid">Paid</SelectItem>
                          <SelectItem value="Freemium">Freemium</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <div>
                    <Label>Website URL</Label>
                    <Input type="url" value={formData.url} onChange={(e) => setFormData({...formData, url: e.target.value})} required />
                  </div>
                  <div>
                    <Label>Image URL</Label>
                    <Input type="url" value={formData.image} onChange={(e) => setFormData({...formData, image: e.target.value})} required />
                  </div>
                  <div>
                    <Label>Tags (comma-separated)</Label>
                    <Input value={formData.tags} onChange={(e) => setFormData({...formData, tags: e.target.value})} placeholder="#AI, #Productivity" required />
                  </div>
                  <div className="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id="featured" 
                      checked={formData.featured} 
                      onChange={(e) => setFormData({...formData, featured: e.target.checked})}
                      className="w-4 h-4"
                    />
                    <Label htmlFor="featured" className="cursor-pointer">Featured Tool</Label>
                  </div>
                  <div className="flex gap-2 pt-4">
                    <Button type="submit" className="bg-pink-600 hover:bg-pink-700 text-white flex-1">
                      {editingTool ? 'Update Tool' : 'Add Tool'}
                    </Button>
                    <Button type="button" variant="outline" onClick={() => setIsAddDialogOpen(false)} className="flex-1">
                      Cancel
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Pricing</TableHead>
                    <TableHead>Featured</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {tools.map(tool => (
                    <TableRow key={tool.id}>
                      <TableCell className="font-medium">{tool.name}</TableCell>
                      <TableCell>
                        <Badge variant="secondary" className="bg-teal-500 text-white">
                          {tool.category}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{tool.pricing}</Badge>
                      </TableCell>
                      <TableCell>
                        {tool.featured && <Badge className="bg-yellow-500 text-white">Featured</Badge>}
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Button size="sm" variant="outline" onClick={() => handleEdit(tool)}>
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button size="sm" variant="outline" className="text-red-600 hover:bg-red-50" onClick={() => handleDelete(tool.id)}>
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;
